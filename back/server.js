const fs = require('fs');
const path = require('path');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const conn = require('./connect/mariadb');
const app = express();

// 설정 파일의 경로
const configPath = path.join(__dirname, '.', 'config.json');

// 설정 파일 읽기
const configData = fs.readFileSync(configPath, 'utf8');
const config = JSON.parse(configData);

// 서버 설정 가져오기
const serverConfig = config.server;

// CORS 설정
app.use(cors({ origin: serverConfig.host+':'+serverConfig.port }));
app.use(express.json());

const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: serverConfig.host+':'+serverConfig.port,
    methods: ['GET', 'POST']
  }
});
app.post('/signup', (req, res) => {
  const { id, pw, name, birth } = req.body;
  const currentDate = new Date();

  const query1 = 'select * from tb_user where user_id = ?';
  conn.query(query1, [id], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      res.status(500).send('Error select data into database');
    } else {
      if (result.length > 0) {
        res.status(300).send('중복된 아이디 입니다.');
      } else {
        const query2 = 'INSERT INTO tb_user (user_id, user_pw, name, birth, insert_date) VALUES (?, ?, ?, ?, ? )';
        conn.query(query2, [id, pw, name, birth, currentDate], (err, result) => {
          if (err) {
            console.error("Database insert error:", err);
            res.status(500).send('Error inserting data into database');
          } else {
            res.status(200).send('User data inserted successfully');
          }
        });
      }
    }
  });
});

app.post('/findIdPw', (req, res) => {
  const { name, birth } = req.body;
  const query = 'select * from tb_user where name = ? and birth = ?';
  conn.query(query, [name, birth], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      res.status(500).send('Error select data into database');
    } else {
      if (result.length > 0) {
        res.status(200).json(result);
      } else {
        res.status(300).send('가입된 아이디가 없습니다.');
      }
    }
  });
});

app.post('/login', (req, res) => {
  const { id, pw } = req.body;
  const query = 'select * from tb_user where user_id = ? and user_pw = ?';
  conn.query(query, [id, pw], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      res.status(500).send('Error select data into database');
    } else {
      if (result.length > 0) {
        res.status(200).json(result);
      } else {
        res.status(300).send('아이디 or 비밀번호가 없습니다.');
      }
    }
  });
});
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
app.post('/loadUserList', (req, res) => {
  const { id } = req.body;
  const query = 'select * from tb_user where id != ?';
  conn.query(query, [id], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      res.status(500).send('Error select data into database');
    } else {
      if (result.length > 0) {
        res.status(200).json(result);
      } else {
        res.status(300).send('아이디 or 비밀번호가 없습니다.');
      }
    }
  });
});

app.post('/loadChatList', (req, res) => {
  const { id } = req.body;
  const query = `select *,
                        (SELECT name FROM tb_user WHERE a.user_id = id) AS user_name,
                        (SELECT img FROM tb_user WHERE a.user_id = id) AS user_img,
                        (SELECT name FROM tb_user WHERE a.other_user_id = id) AS other_user_name,
                        (SELECT img FROM tb_user WHERE a.other_user_id = id) AS other_user_img
                 from tb_chat a
                 where a.user_id = ?`;

  conn.query(query, [id], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      res.status(500).send('Error select data into database');
    } else {
      if (result.length > 0) {
        res.status(200).json(result);
      } else {
        res.status(200).json({msg:'챗봇 방이없습니다.'});
      }
    }
  });
});


app.post('/loadProfile', (req, res) => {
  const { id } = req.body;
  const query = 'select * from tb_user where id = ? ';
  conn.query(query, [id], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      res.status(500).send('Error select data into database');
    } else {
      if (result.length > 0) {
        res.status(200).json(result);
      } else {
        res.status(300).send('아이디 or 비밀번호가 없습니다.');
      }
    }
  });
});

app.post('/updateProfile', (req, res) => {
  const { id, user_pw, name, birth, comments, img } = req.body;

  const query = 'UPDATE tb_user SET user_pw = ?, name = ?, birth = ?, comments = ?, img = ? WHERE id = ?';
  conn.query(query, [user_pw, name, birth, comments, img, id], (err, result) => {
    if (err) {
      console.error("Database update error:", err);
      res.status(500).send('Error updating data in the database');
    } else {
      res.status(200).send('Profile updated successfully');
    }
  });
});

app.post('/createChat', (req, res) => {
  const { myid, myimg, otherid, otherimg } = req.body;

  const query1 = 'SELECT * FROM tb_chat WHERE user_id = ? AND other_user_id = ?';
  conn.query(query1, [myid, otherid], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      return res.status(500).send('Error selecting data from database');
    }else if (result.length > 0) {
      return res.status(200).json(result);
    } else {
      const randomString = generateRandomString(13);
      const query2 = 'INSERT INTO tb_chat (user_id, other_user_id, room, img) VALUES (?, ?, ?, ?), (?, ?, ?, ?)';
      conn.query(query2, [myid, otherid, randomString, myimg, otherid, myid, randomString, otherimg], (err, result) => {
        if (err) {
          console.error("Database insert error:", err);
          return res.status(500).send('Error inserting data into the database');
        }
        res.status(200).json( {room: randomString} );
      });
    }
  });
});

app.post('/msgListAdd', (req, res) => {
  const { room, text, sender, id, otherid, img } = req.body;

  if (otherid !== '' && otherid !== null && otherid !== undefined) {
    const query = 'insert into tb_log_chat ( user_name, user_type, other_name, room, msg, img)value(?,?,?,?,?,?)';
    conn.query(query, [id, sender, otherid, room, text, img], (err, result) => {
      if (err) {
        console.error("Database insert error:", err);
        res.status(500).send('Error insert data in the database');
      } else {
        res.status(200).send('msgListAdd insert successfully');
      }
    });
  }else{
    res.status(200).send('data X');
  }


});

app.post('/loadMsgList', (req, res) => {
  const { user_name, room } = req.body;

  const query = 'select user_name, user_type, other_name, msg, img from tb_log_chat where user_name=? and room = ? order by insertdate';
  conn.query(query, [user_name, room], (err, result) => {
    if (err) {
      console.error("Database select error:", err);
      res.status(500).send('Error select data in the database');
    } else {
      if (result.length > 0) {
        res.status(200).json(result);
      }else{
        // res.status(300).send('No data loadMsgList select');
      }
      
    }
  });
});



io.on('connection', (socket) => {
  console.log('A user connected');

  socket.on('join room', (room, senderName) => {
    socket.join(room);
    // const msg = `${senderName}님이 방에 참여했습니다.`;
    // socket.to(room).emit('bot', { msg });
  });

  socket.on('user', (room, msg, senderName, img) => {
    io.to(room).emit('chat message', { msg, senderName, img });
  });

  socket.on('leave room', (room) => {
    socket.leave(room);
    console.log(`User left room: ${room}`);
  });

  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

server.listen(3000, () => {
  console.log(`Server running`);
});

function generateRandomString(length) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

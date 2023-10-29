const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000;

// 设置静态文件目录
app.use(express.static('public'));


app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html'); // 替换为您的HTML文件路径
});


// 实现硬超时
app.get('/timeout', (req, res) => {
  exec('python public/timeout.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`执行 timeout.py 出错：${error.message}`);
      return res.status(500).send('执行出错');
    }
    console.log(`timeout.py 输出：${stdout}`);
    res.send(stdout);
  });
});

// 获取s1上实时的流表数
app.get('/getflow', (req, res) => {
  exec('python public/getflow.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`执行 getflow.py 出错：${error.message}`);
      return res.status(500).send('执行出错');
    }
    console.log(`getflow.py 输出：${stdout}`);
    res.send(stdout);
  });
});

// 删除流表项
app.get('/delete', (req, res) => {
  exec('python public/delete.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`执行 delete.py 出错：${error.message}`);
      return res.status(500).send('执行出错');
    }
    console.log(`delete.py 输出：${stdout}`);
    res.send(stdout);
  });
});

// 获取拓扑信息
app.get('/getinfo', (req, res) => {
  exec('python public/getinfo.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`执行 getinfo.py 出错：${error.message}`);
      return res.status(500).send('执行出错');
    }
    console.log(`getinfo.py 输出：${stdout}`);
    res.send(stdout);
  });
});

// 在s1和s2上添加流表，划分VLAN
app.get('/vlan', (req, res) => {
  exec('python public/vlan.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`执行 vlan.py 出错：${error.message}`);
      return res.status(500).send('执行出错');
    }
    console.log(`vlan.py 输出：${stdout}`);
    res.send(stdout);
  });
});

// 查看流表项
app.get('/getflows', (req, res) => {
  exec('python public/getflows.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`执行 getflows.py 出错：${error.message}`);
      return res.status(500).send('执行出错');
    }
    console.log(`getflows.py 输出：${stdout}`);
    res.send(stdout);
  });
});

// 启动服务器
app.listen(port, () => {
  console.log(`服务器已启动，监听端口 ${port}`);
});

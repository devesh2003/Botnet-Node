var express = require('express');
var bodyParser = require('body-parser');


var app = express();
var urlEncodedParser = bodyParser.urlencoded({extended:false});

app.set('view engine','ejs');

app.use('/',express.static('./public'))

app.get('/',function(req,resp){
    resp.render('login');
});

app.post('/login',urlEncodedParser,function(req,resp){
    if (req.body.username === 'baapo'){
        console.log('Username Ok');
        if (req.body.pass === 'deveshisgreat'){
            console.log('Password Ok')
            resp.render('CnC');
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
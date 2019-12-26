const { exec } = require('child_process');

exec('dir',(error,t,a) => {
    console.log(t);
});
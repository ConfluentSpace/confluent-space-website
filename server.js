var express = require('express')
var app = express()

app.use(express.static("site"));
console.log("Now listening on http://localhost:3000")
app.listen(3000);

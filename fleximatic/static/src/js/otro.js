$.ajax({
    url: 'https://fleximatic-s-1-1426819.dev.odoo.com/web/session/authenticate',
    headers: {
        'Content-Type':'application/json',
    },
    method: 'POST',
    data: JSON.stringify({"jsonrpc":2.0,"method":"call","params":{"service":"common","method":"login", 'db':'fleximatic-s-1-1426819','login':'admin','password':'admin' },"id":5}),
    success: function(data, status, xhr){
       console.log(data);
    },
    error: function(error) {
    console.log(error)
}
  });

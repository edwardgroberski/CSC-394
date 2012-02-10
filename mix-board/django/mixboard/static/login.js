(function() {
  function getURLParameter(name) {
  return decodeURI(
      (RegExp('[?|&]' + name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
  );
};
  $(document).ready(function() {
    $('#loginForm').submit(function(e) {
      var next, password, postData, url, username;
      e.preventDefault();
      username = $('#loginName').val();
      password = $('#loginPassword').val();
      url = $('#loginForm').attr('action');
      next = getURLParameter('next');
      postData = {
        'username': username,
        'password': password
      };
      return $.post(url, postData, function(response) {
        switch (response) {
          case 'success':
            if (!(next != null) || next === "null") {
              return window.location.replace(window.location.pathname);
            } else {
              return window.location.href = next;
            }
            break;
          default:
            return $('#loginError').html(response);
        }
      });
    });
    $('#logoutButton').click(function(e) {
      return $.post('/logout/', '', function(response) {
        return window.location.href = '/';
      });
    });
    $('#profileButton').click(function(e) {
      return window.location.href = "/user/profile/" + ($('#userid').html()) + "/" + ($('#username').html()) + "/";
    });
    $('#usersButton').click(function(e) {
      return window.location.href = '/user/list/';
    });
    return $('#trendingButton').click(function(e) {
      return window.location.href = '/song/trending/';
    });
  });

}).call(this);

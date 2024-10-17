document.getElementById('toggleSidebar').addEventListener('click', function() {
  var sidebar = document.getElementById('sidebar');
  var backdrop = document.getElementById('backdrop');
  sidebar.classList.toggle('show');
  backdrop.classList.toggle('show');
});

document.getElementById('backdrop').addEventListener('click', function() {
  var sidebar = document.getElementById('sidebar');
  var backdrop = document.getElementById('backdrop');
  sidebar.classList.remove('show');
  backdrop.classList.remove('show');
});



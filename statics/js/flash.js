const alertList = document.querySelectorAll(".alert");
alertList.forEach(function (alert) {
  new bootstrap.Alert(alert);
});

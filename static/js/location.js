function make_table_editable(id) {
  const val = document.getElementById(id).value;
  document.getElementById(val).removeAttribute("hidden");
  document.getElementById('edit' + val).setAttribute("disabled", "");
  document.getElementById('delete' + val).setAttribute("disabled", "");
  var td_loc = 'td' + val;
  var tds = document.getElementsByName(td_loc);

  for (var i = 0; i < tds.length; i++) {
    tds.item(i).setAttribute("contenteditable", "true");
  }
}
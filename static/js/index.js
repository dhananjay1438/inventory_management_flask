function validate_data() {
  var to_location = document.getElementById("to_location");
  var from_location = document.getElementById("from_location");
  if (from_location.value == '' && to_location.value == '') {
    alert("Atleast one out of two (from location and to location) must be filled");
  }
}

function make_table_editable(id) {
  const val = document.getElementById(id).value;
  document.getElementById(val).removeAttribute("hidden");
  document.getElementById('edit' + val).setAttribute("disabled", "");
  document.getElementById('delete' + val).setAttribute("disabled", "");
  var td_loc = 'td' + val;
  var tds = document.getElementsByName(td_loc);

  for (var i = 0; i < tds.length; i++) {
    if (i == 0 || i == 1) {
      continue;
    }
    tds.item(i).setAttribute("contenteditable", "true");
  }
}

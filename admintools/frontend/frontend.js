$(function() {

  // Test if already loged in
  loading();
  testLogin();

  // Pressed login button
  $("#loginbutton").on("click", function(){
    localStorage.setItem('telephone', $("#telephone").val());
    localStorage.setItem('code', "");
    loading();
    testLogin();
  });

  // Pressed the code button
  $("#codebutton").on("click", function(){
    localStorage.setItem('code', $("#code").val());
    loading();
    testLogin();
  });

  // Pressed the code button
  $("#passwordbutton").on("click", function(){
    localStorage.setItem('password', $("#password").val());
    $("#password").val("");
    loading();
    testLogin();
  });

  // Pressed group button
  $("#groupbutton").on("click", function(){
    localStorage.setItem('groupid', $("#group").val());
    localStorage.setItem('grouptitle', $("#group").find("option[value=" + $("#group").val() + "]").html());
    loading();
    getParticipants();
  });

  // Pressed delete group button
  $("#deletegroupbutton").on("click", function(){
    localStorage.removeItem('groupid');
    localStorage.removeItem('grouptitle');
    localStorage.removeItem('participants');
    loading();
    getChats();
  });

  // Another action button
  $(".anotheractionbutton").on("click", function(){
    loading();
    show_section("actions");
  });

  // Logout button
  $("#logoutbutton").on("click", function(){
    localStorage.removeItem('telephone');
    localStorage.removeItem('code');
    loading();
    $.get("/data/logout",function(r){
      show_section("auth");
    });
  });

  // Start over button
  $("#startoverlink").on("click",function(){
    localStorage.clear();
    window.location.reload();
  });

  // Hide or show action period
  show_hide_action_period = function(){
    var action = $("#action").val();
    if (action == "0" || action == "3"){
      $("#period").prop("disabled", true);
      $('select').formSelect();
    }
    else{
      $("#period").prop("disabled", false);
      $('select').formSelect();
    }
  };
  $("#action").on("change", show_hide_action_period);
  show_hide_action_period();

  // Pressed action button
  $("#actionbutton").on("click", function(){
    var action = $("#action").val();
    if (action == "0"){
      loading();
      $("#notvalidated-table tr").not(".default").remove();
      $.get("/data/getnotvalidated/" + localStorage.getItem("groupid"), null, function(response, ts, jq){
        response.forEach(function(val, i, a){
          var newrow = $("<tr></tr>");
          $($($("<td></td>")).html(val["id"])).appendTo(newrow);
          $($($("<td></td>")).html(val["username"])).appendTo(newrow);
          $($($("<td></td>")).html(val["first_name"])).appendTo(newrow);
          $($($("<td></td>")).html(val["last_name"])).appendTo(newrow);
          $(newrow).appendTo($("#notvalidated-table"));
        });
        show_section("action-notvalidated", jq.getResponseHeader('X-last-fetched-data'));
      }, "json");
    }
    else if (action == "1"){
      loading();
      $("#inactive-table tr").not(".default").remove();
      var period = $("#period").val();
      $.get("/data/getinactive/" + localStorage.getItem("groupid") + "/" + period, null, function(response, ts, jq){
        response.forEach(function(val, i, a){
          var newrow = $("<tr></tr>");
          $($($("<td></td>")).html(val["id"])).appendTo(newrow);
          $($($("<td></td>")).html(val["username"])).appendTo(newrow);
          $($($("<td></td>")).html(val["first_name"])).appendTo(newrow);
          $($($("<td></td>")).html(val["last_name"])).appendTo(newrow);
          $(newrow).appendTo($("#inactive-table"));
        });
        show_section("action-inactive", jq.getResponseHeader('X-last-fetched-data'));
      }, "json");
    }
    else if (action == "3"){
      loading();
      $("#teams-table tr").not(".default").remove();
      $.get("/data/getteams/" + localStorage.getItem("groupid"), null, function(response, ts, jq){
        // Fill in table
        var labels = {
          "Rojo": "Red",
          "Azul": "Blue",
          "Amarillo": "Yellow",
          "Desconocido": "Unknown"
        }
        for (var key in response) {
          var newrow = $("<tr></tr>");
          $($($("<td></td>")).html(labels[key])).appendTo(newrow);
          $($($("<td></td>")).html(response[key])).appendTo(newrow);
          $(newrow).appendTo($("#teams-table"));
        }
        // Draw chart
        var ctx = document.getElementById("teams-chart").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ["Red", "Blue", "Yellow", "Unknown"],
                datasets: [{
                    label: '# of users',
                    data: [response["Rojo"], response["Azul"], response["Amarillo"], response["Desconocido"]],
                    backgroundColor: [
                      'rgba(255,0,0,0.7)',
                      'rgba(0, 0, 255, 0.7)',
                      'rgba(255, 255, 0, 0.7)'
                    ],
                    borderColor: [
                        'rgba(200,0,0,1)',
                        'rgba(0, 0, 200, 1)',
                        'rgba(200, 200, 0, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
              legend: {
                display: false
              }
            }
        });
        show_section("action-teams", jq.getResponseHeader('X-last-fetched-data'));
      }, "json");
    }
    else if (action == "4"){
      loading();
      $("#gyms-table tr").not(".default").remove();
      var period = $("#period").val();
      $.get("/data/getgyms/" + localStorage.getItem("groupid") + "/" + period, null, function(response, ts, jq){
        response.forEach(function(val, i, a){
          var newrow = $("<tr></tr>");
          var tags = "";
          if(val["tags"].toLowerCase().indexOf("ex")>-1) tags+="🌟";
          if(val["tags"].toLowerCase().indexOf("parque")>-1) tags+="🌳";
          if(val["tags"].toLowerCase().indexOf("jardin")>-1) tags+="🌷";
          if(val["tags"].toLowerCase().indexOf("juegos")>-1) tags+="⚽️";
          if(val["tags"].toLowerCase().indexOf("hierba")>-1) tags+="🌱";
          if(val["tags"].toLowerCase().indexOf("campo")>-1) tags+="🌱";
          if(val["tags"].toLowerCase().indexOf("patrocinado")>-1) tags+="💵";
          $($($("<td></td>")).html(val["id"])).appendTo(newrow);
          $($($("<td></td>")).html(val["name"])).appendTo(newrow);
          $($($("<td></td>")).html(val["count"])).appendTo(newrow);
          $($($("<td></td>")).html(val["people"])).appendTo(newrow);
          $($($("<td></td>")).html(tags)).appendTo(newrow);
          $(newrow).appendTo($("#gyms-table"));
        });
        show_section("action-gyms", jq.getResponseHeader('X-last-fetched-data'));
      }, "json");
    }
  });

  // Press export button (generalized for all buttons)
  $(".exportbutton").on("click", function(){
    var currentact = $(this).attr("data-action");
    var filename = currentact + localStorage.getItem("groupid") + "_" + new Date().getTime() + ".csv";
    CSV_EXPORT = Array();
    var rows = $(this).parent().parent().find("table tr").not(".default");
    $.each(rows, function(key, val){
      var vals = $(val).find("td");
      var row = ""
      $.each(vals, function(key2, val2){
        row = row + $(val2).html() + "\t";
      });
      row = row.substring(0, row.length - 1);
      CSV_EXPORT = CSV_EXPORT + row + "\n"
    });
    CSV_EXPORT = CSV_EXPORT.substring(0, CSV_EXPORT.length - 1);
    var blob = new Blob([CSV_EXPORT], {
      type: "text/plain;charset=utf-8"
    });
    saveAs(blob, filename);
  });

  // UI Initialization
  $('select').formSelect();
  $('.tooltipped').tooltip();

});

function testLogin(){
  data = {
    "telephone": localStorage.getItem("telephone"),
    "code": localStorage.getItem("code"),
    "password": localStorage.getItem("password"),
    "g-recaptcha-response": $("#g-recaptcha-response").val()
  };
  if(data.telephone==null){
    show_section("auth");
  }
  else{
    $.ajax({
      type: "POST",
      url: "/data/auth",
      data: data,
      success: function(response, ts, jq){
        if(response == "ok_alreadyauthorized" || response == "ok_signedin"){
          if(localStorage.getItem("participants") && localStorage.getItem("grouptitle") && localStorage.getItem("groupid")){
            show_section("actions", jq.getResponseHeader('X-last-fetched-data'));
          }
          else{
            getChats();
          }
        }
        else if(response == "checkphone"){
          show_section("code");
        }
        else if(response == "needpassword"){
          show_section("password");
        }
        else if(response == "badphone"){
          localStorage.removeItem('telephone');
          localStorage.removeItem('code');
          window.alert("Invalid phone number. Please enter your phone in international convention format, e.g. '+34600111222'");
          show_section("auth");
        }
        else if(response == "norecaptcha"){
          localStorage.removeItem('telephone');
          localStorage.removeItem('code');
          window.alert("Please pass the recaptcha challenge before attempting to continue");
          show_section("auth");
        }
        else if(response == "badrecaptcha"){
          localStorage.removeItem('telephone');
          localStorage.removeItem('code');
          window.alert("Sorry mate, recaptcha is invalid");
          show_section("auth");
        }
        else if(response == "badcode"){
          window.alert("Invalid code entered. Please enter a valid code to continue!");
          show_section("code");
        }
        else if(response == "badpassword"){
          window.alert("Invalid password entered. Please enter your password to continue!");
          show_section("password");
        }
        else if(response == "pleasecooldown"){
          show_error("Too much requests from you! Please try again after some hours.");
        }
        else if(response == "cantsendcode"){
          show_error("Too much login attempts from you! Please try again after some hours.");
        }
        else{
          localStorage.removeItem('telephone');
          localStorage.removeItem('code');
          window.alert("Unknown error");
          show_section("auth");
        }
      },
      dataType: "text",
      error: function(){
        show_error("Received error from server. Please try again later.");
      }
    });
  }
}

function getChats(){
  $.get("/data/getchats", null, function(response, ts, jq){
    if(response == "pleasecooldown"){
      show_error("Too much requests! Please try again after some hours.");
      return;
    }
    show_section("group", jq.getResponseHeader('X-last-fetched-data'));
    $("#group option").not(".default").remove();
    response.forEach(function(val, i, a){
      var newoption = $("<option></option>");
      $(newoption).attr("value", val[0]);
      $(newoption).html(val[1]);
      $(newoption).appendTo($("#group"));
    });
    $('select').formSelect();
  }, "json");
}

function getParticipants(){
  groupid = localStorage.getItem("groupid");
  $.get("/data/getparticipants/" + groupid, null, function(response, ts, jq){
    if(response == "ok"){
      $("#group option").not(".default").remove();
      show_section("actions", jq.getResponseHeader('X-last-fetched-data'));
    }
    else if(response == "error_unknownchat"){
      show_errort("Specified chat is not in your opened chats");
    }
    else if(response == "error_cantfindchat"){
      show_error("Can't find specified chat. Maybe you closed it?");
    }
    else if(response == "pleasecooldown"){
      show_error("Too much requests! Please try again after some hours.");
      return;
    }
  }, "text");
}

function loading(){
  $(".section").addClass("hide");
  $(".section-loading").removeClass("hide");
}

function show_section(what, updatedago){
  if(what == "actions"){
    $(".grouptitle-show").html(localStorage.getItem("grouptitle"));
  }
  $(".section").addClass("hide");
  $(".section-" + what).removeClass("hide");
  if(typeof(updatedago)!="undefined")
    $(".section-" + what + " .lastupdate").html(jQuery.timeago(updatedago));
}

function show_error(what){
  $(".section").addClass("hide");
  $(".section-error p.error-text").html(what);
  $(".section-error").removeClass("hide");
}

/* 
To automate your slack instance invites,
1. Create a google form with two text fields:
"Your email"
"Who invite you"
2. You will get a google table with responses and 3 fields:
1) "Timestamp"  
2) "Your email"
3) "Who invite you"
3. From the resultant google sheet, go to "Tools" -> "Script Editor"
// kudos to @sugavaneshb for the note:
// "Tools -> Script Editor" option has to be chosen from the resultant google sheet and not from form. Else, there will be no 'active spreadsheet' when trying to run/initialize from form.
4. Copy-paste this script.
5. Populate secrets strings (see below) by your very own values.
6. Click "Run" -> "Initialize"
Congratulations, you are successfully rool-out invite automation!
*/

// secrets
var SlackName = 'totalgood'; // name of your slack
var SlackToken = 'xoxs-359****'; // Slack auth token 
var ccEmail = 'slack+signups@totalgood.com'; // your email, if you want to get email notification (otherwise comment out SendEmail call)
// end secrets

function Initialize() {
 
  var triggers = ScriptApp.getProjectTriggers();
 
  for (var i in triggers) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
 
  ScriptApp.newTrigger("onFormSubmitEx")
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onFormSubmit()
    .create();
 
}

function post(url, payload) {
  
  var options =
      {
        "method"  : "POST",
        "payload" : payload,   
        "followRedirects" : true,
        "muteHttpExceptions": true
      };
  
  var result = UrlFetchApp.fetch(url, options);
  return result.getContentText();
}

// send email to your ccEmail with sign-up info
function SendMail(newEmail, whoInvite, curlStatus) {
 
  try {
    // This will show up as the sender's name
    sendername = "Slack auto-invite";
 
    // Optional but change the following variable
    // to have a custom subject for Google Docs emails
    subject = "New user signed up";
 
    // This is the body of the auto-reply
    message = "New user <b>" +  newEmail + "</b> signed up<br><br>";
    message += 'Invited by  :: ' + whoInvite + "<br>";
    message += 'Curl status :: ' + curlStatus + "<br>";
 
    textbody = message.replace("<br>", "\n");
 
    GmailApp.sendEmail(ccEmail, subject, textbody, {
      cc: ccEmail,
      name: sendername,
      htmlBody: message
    });
 
  } catch (e) {
    Logger.log(e.toString());
  }
 
}

function onFormSubmitEx(e) {

  var timestamp = e.values[0];
  var toAddress = e.values[1];
  var whoInvite = e.values[2];
  var slackInviteUrl = 'https://' + SlackName + '.slack.com/api/users.admin.invite';
  
  var curlStatus = post(slackInviteUrl, {
    token: SlackToken,
    email: toAddress
  });
  SendMail(toAddress, whoInvite, curlStatus);
}
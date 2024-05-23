document.getElementById('theme-toggle').addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
});

const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('chat-input');
const sendButton = document.getElementById("send-button");

const inactiveMessage = "Server is down, Please contact the developer to activate it";
var host = "http://localhost:5005/webhooks/rest/webhook";
let passwordInput = false;

messageInput.addEventListener("keydown", (event) => {
if (event.key === "Enter") {
  event.preventDefault();
  sendButton.click();
}
});

function replaceWithAsterisks(str) {
  return '*'.repeat(str.length);
}

function userResponseBtn(e) {
send(e.value);
}

function send(message) {
  messageInput.type = "text"
  passwordInput = false;
  messageInput.focus();
  console.log("User Message:", message)

  // Disable the input field while the AJAX request is in progress
  messageInput.disabled = true;

  $.ajax({
      url: host,
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
          "message": message,
          "sender": "User"
      }),
      success: function(data, textStatus) {
          if (data != null) {
            setBotResponse(data);
          }
          console.log("Rasa Response: ", data, "\n Status:", textStatus)
          // Enable the input field after the AJAX request has completed
          messageInput.disabled = false;
      },
      error: function(errorMessage) {
          setBotResponse("");
          console.log('Error' + errorMessage);

          // Enable the input field after the AJAX request has completed
          messageInput.disabled = false;

      }
  });
}

function createChatBubble(message) {
  const botMessage = document.createElement('div');
  botMessage.classList.add('chat-message', 'bot-message');
  botMessage.innerHTML = `<span>🤖 "${message}"</span>`;
  return botMessage
}

function createImageBubble(imageUrl) {
  const botMessage = document.createElement('div');
  botMessage.classList.add('chat-message', 'bot-message');
  const image = document.createElement("img");
  image.src = imageUrl;
  botMessage.appendChild(image);
  return botMessage
}

function createButton(buttonData) {
  const button = document.createElement("button");
  button.classList.add("btn-primary");
  button.textContent = buttonData.title;
  button.value = buttonData.payload;
  button.addEventListener("click", function() {
      userResponseBtn(this);
  });
  return button;
}

function setBotResponse(val) {
  setTimeout(function() {
      if (val.length < 1) {
          // If there is no response from Rasa
          const msg = inactiveMessage;
          chatBox.appendChild(createChatBubble(msg));
      } else {
          // If we get response from Rasa
          for (let i = 0; i < val.length; i++) {
              if (val[i].hasOwnProperty("text")) {
                  const botMsg = val[i].text.toLowerCase();
                  if (botMsg.includes("password")) {
                      messageInput.type = "password";
                      passwordInput = true;
                  }
                  chatBox.appendChild(createChatBubble(botMsg));
              }

              if (val[i].hasOwnProperty("image")) {
                  const botMsg = val[i].image;
                  chatBox.appendChild(createImageBubble(botMsg));
              }

              if (val[i].hasOwnProperty("buttons")) {
                  const buttons = val[i].buttons;
                  buttons.forEach(btn => {
                      chatBox.appendChild(createButton(btn));
                  });
              }
          }
      }
  }, 1000);
}

function displaythumbnail(file){
  //This is to display the uploaded file thumbnail
  const fileType = file.type.split("/")[0];
  let thumbnail;
  if (fileType === "image") {
    thumbnail = document.createElement("img");
    thumbnail.src = URL.createObjectURL(file);
    thumbnail.alt = file.name;
  } else {
    thumbnail = document.createElement("i");
    thumbnail.classList.add("fas", "fa-file-alt");
  }

  const thumbnailBubble = document.createElement("div");
  thumbnailBubble.classList.add('chat-message', 'bot-message', 'file-bubble');
  thumbnailBubble.appendChild(thumbnail);

  // Appending the bot bubble to the chat area
  setTimeout(() => {
    chatBox.appendChild(thumbnailBubble);
  }, 500);
}

sendButton.addEventListener("click", () => {
  const message = messageInput.value.trim();
  if (message !== "") {
      // This is for creating a chat bubble for the user message
      const userMessage = document.createElement('div');
      userMessage.classList.add('chat-message', 'user-message');
      if (passwordInput) {
        userMessage.textContent = replaceWithAsterisks(message);
        messageInput.value = "";
      }
      if (message) {
          userMessage.textContent = message;
          // This is to clear the input field
          messageInput.value = "";
      }

      chatBox.appendChild(userMessage);
      send(message)

      chatBox.scrollTop = chatBox.scrollHeight;
  }
});

//For Handling File uploads
const fileUpload = document.getElementById("upload-file");

fileUpload.addEventListener("change", (event) => {
  if (event.target.files.length > 0) {
      const file = event.target.files[0];
      let fileInfo = {"name":file.name, "type":file.type, "size":file.size}
      console.log(file.name, file.type, file.size)
      const message = `I just sent a file 📔`;
      // This is for creating a chat bubble for the user message
      const userMessage = document.createElement("div");
      userMessage.classList.add('chat-message', 'user-message');
      userMessage.textContent = message;

      // This is for appending the user bubble to the chat area
      const chatBox = document.getElementById('chat-box');
      chatBox.appendChild(userMessage);

      // This is for clearing the input field
      messageInput.value = "";
      displaythumbnail(file)
      send(JSON.stringify(fileInfo))
      chatBox.scrollTop = chatBox.scrollHeight;

  } 
  else {
      const botMessage = document.createElement("div");
      botMessage.classList.add('chat-message', 'bot-message');
      botMessage.textContent = `You did not upload any File.`;
      chatBox.appendChild(botMessage);
      console.log("No file selected");
  }
});  


function restartChat() {
  const userMessage = document.createElement('div');
  userMessage.classList.add('chat-message', 'user-message');
  userMessage.textContent = "/restart";
  chatBox.append(userMessage)
  send("/restart")
  chatBox.scrollTop = chatBox.scrollHeight;
  chatBox.innerHTML = '';
}

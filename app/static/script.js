document.getElementById('send-btn').addEventListener('click', function() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `message=${message}`
    })
    .then(response => response.json())
    .then(data => {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML += `<p><strong>You:</strong> ${data.user_message}</p>`;
        messagesDiv.innerHTML += `<p><strong>AI:</strong> ${data.ai_response}</p>`;
        messageInput.value = '';
    });
});

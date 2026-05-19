function login(){

    const id = document.getElementById("loginId").value;

    const pw = document.getElementById("loginPw").value;

    if(id === "" || pw === ""){
        alert("아이디와 비밀번호를 입력하세요.");
        return;
    }

    alert("로그인 성공!");

    location.href = "team.html";
}



function signup(){

    const id = document.getElementById("signupId").value;

    const pw = document.getElementById("signupPw").value;

    const pw2 = document.getElementById("signupPw2").value;

    const name = document.getElementById("signupName").value;

    const email = document.getElementById("signupEmail").value;

    if(id === "" || pw === "" || pw2 === "" || name === "" || email === ""){
        alert("모든 정보를 입력하세요.");
        return;
    }

    if(pw !== pw2){
        alert("비밀번호가 다릅니다.");
        return;
    }

    alert("회원가입 완료!");

    location.href = "index.html";
}



function createTeam(){

    const teamName = document.getElementById("teamName").value;

    const teamInfo = document.getElementById("teamInfo").value;

    const teamMember = document.getElementById("teamMember").value;

    const teamLeader = document.getElementById("teamLeader").value;

    if(teamName === "" || teamInfo === "" || teamMember === "" || teamLeader === ""){
        alert("팀 정보를 모두 입력하세요.");
        return;
    }

    alert("팀 생성 완료!");
}
function sendMessage(){

    const input = document.getElementById("messageInput");

    const chatBox = document.getElementById("chatBox");

    const text = input.value;

    if(text.trim() === ""){
        return;
    }

    const message = document.createElement("div");

    message.className = "message me";

    message.innerHTML = text;

    chatBox.appendChild(message);

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;
}



const inputField = document.getElementById("messageInput");

let isComposing = false;



inputField.addEventListener("compositionstart", () => {
    isComposing = true;
});



inputField.addEventListener("compositionend", () => {
    isComposing = false;
});



inputField.addEventListener("keydown", function(event){

    if(event.key === "Enter" && !isComposing){

        event.preventDefault();

        sendMessage();
    }

});
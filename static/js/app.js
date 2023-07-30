firebase.initializeApp({
    apiKey: "AIzaSyBSbk98fPAhAGc_yCUQ82TAXlxzSMATvlM" ,
    authDomain: "flaskblog-8053a.firebaseapp.com",
    projectId: "flaskblog-8053a"
});

function register() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((userCredential) => {
            console.log("Registro exitoso. Bienvenido, " + userCredential.user.email);
        })
        .catch((error) => {
            console.error("Error en el registro:", error.message);
        });
}
function login() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    firebase.auth().signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            console.log("Inicio de sesión exitoso. Bienvenido, " + userCredential.user.email);
        })
        .catch((error) => {
            console.error("Error en el inicio de sesión:", error.message);
        });
}
firebase.initializeApp(firebaseConfig);




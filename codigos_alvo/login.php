<?php
// Script de Login Vulnerável para Teste do Gate of Babylon
$usuario = $_POST['username'];
$senha = $_POST['password'];

// Conexão simulada
$conn = new mysqli("localhost", "root", "", "banco_teste");

// Falha 1: SQL Injection clássico
$query = "SELECT * FROM usuarios WHERE username = '$usuario' AND password = '$senha'";
$resultado = $conn->query($query);

if ($resultado->num_rows > 0) {
    // Falha 2: Reflected XSS
    echo "<h1>Bem vindo, " . $usuario . "!</h1>";
} else {
    echo "Login falhou.";
}
?>

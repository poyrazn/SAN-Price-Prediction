<?php
// Veritabanı Bağlantısı
try{
    $db = new PDO('mysql:host=localhost;dbname=sanapi;charset=utf8','root','');
}catch(PDOException $e){
    echo 'Hata: '.$e->getMessage();
}
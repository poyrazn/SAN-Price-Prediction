<?php

/* VAR */
$hotelname = @$_POST['hotelname'];
$departureDate = @$_POST['departureDate'];
$returnDate = @$_POST['returnDate'];


$pythonPath = "C:\Users\DeveloperPC\AppData\Local\Programs\Python\Python37\python.exe";
$pythonScript = "db.py \"{$hotelname}\" {$departureDate} {$returnDate}";

$command = "{$pythonPath} {$pythonScript}";

$lastInsertID = (int) exec($command,$output,$returnval);

if( empty($lastInsertID) || $lastInsertID == 0 || $lastInsertID == null) {
    header('Location: http://localhost/sanapi/');
}else{
    header("Location: http://localhost/sanapi/api.php?id={$lastInsertID}");
}
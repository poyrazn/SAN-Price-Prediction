<?php
require_once "config.php";

$id = $_GET['id'];



$sql = $db->prepare("SELECT * FROM predictions JOIN sandata ON 
    sandata.id = predictions.sandata_id WHERE predictions.id = ?");
$sql->execute(array($id));

$row=$sql->fetchAll(PDO::FETCH_ASSOC);
echo json_encode($row);


?>
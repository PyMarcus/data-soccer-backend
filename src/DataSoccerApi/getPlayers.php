<?php
error_reporting(E_ERROR | E_PARSE);
header("Content-Type:application/json");

$jogadores = Select();
$resposta =[];
foreach($jogadores as $jogador){
  array_push($resposta,$jogador);
}

response(200,"Jogadores encontrados com sucesso",$resposta);

function response($status,$status_message,$data = 'ERROR')
{
	header("HTTP/1.1 ".$status);
	
	$response['status']=$status;
	$response['status_message']=$status_message;
	$response['data']=$data;
	
	$json_response = json_encode($response);
	echo $json_response;
}

function Select(){
	require "DataBase/connection.php";
	$array = [];
	$sql = 'SELECT * FROM `jogador`';
	$stmt = $conn->prepare($sql);
	$stmt->execute();
	$stmt->setFetchMode(PDO::FETCH_ASSOC);

	foreach(new RecursiveArrayIterator($stmt->fetchAll()) as $k=>$row) {
	  array_push($array,$row);
	}
	return $array;
}

?>
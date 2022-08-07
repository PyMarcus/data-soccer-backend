<?php
error_reporting(E_ERROR | E_PARSE);
header("Content-Type:application/json");

$partidas = Select();


$rodadas = [];
$rodada = [];
foreach($partidas as $partida){
    if( $rodadas[$partida['numero_rodada']] != null){
           $rodada = $rodadas[$partida['numero_rodada']];
    }
    
    $disputa = [
        'time_mandante' => $partida['nome_mandante'],
        'time_visitante' => $partida['nome_visitante'],
        'cartao_vermelho_mandante' => $partida['cartao_vermelho_mandante'],
        'cartao_vermelho_visitante' => $partida['cartao_vermelho_visitante'],
        'cartao_amarelo_mandante' => $partida['cartao_amarelo_mandante'],
        'cartao_amarelo_visitante' => $partida['cartao_amarelo_visitante'],
        'gols_mandante' => $partida['gols_mandante'],
        'gols_visitante' => $partida['gols_visitante'],
        'escudo_mandante' => $partida['escudo_mandante'],
        'estadio' => $partida['estadio'],
        'escudo_visitante' => $partida['escudo_visitante']
    ];
    array_push($rodada,$disputa);
    $rodadas[$partida['numero_rodada']] = $rodada;
}
response(200,"Partida encontrada com sucesso",$rodadas);
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
	$sql = 'SELECT disputa.numero_rodada,disputa.clube_id_mandante, disputa.clube_id_visitante, disputa.estadio ,disputa.cartao_vermelho_mandante, disputa.cartao_vermelho_visitante, disputa.cartao_amarelo_mandante, disputa.cartao_amarelo_visitante, disputa.gols_mandante, disputa.gols_visitante, time1.nome AS nome_mandante, time2.nome AS nome_visitante, time1.escudo as escudo_mandante, time2.escudo  as escudo_visitante FROM `disputa` INNER JOIN time time1 ON time1.id_clube=disputa.clube_id_mandante INNER JOIN time time2 ON time2.id_clube=disputa.clube_id_visitante;';
	$stmt = $conn->prepare($sql);
	$stmt->execute();
	$stmt->setFetchMode(PDO::FETCH_ASSOC);
	foreach(new RecursiveArrayIterator($stmt->fetchAll()) as $k=>$row) {
	  array_push($array,$row);
	}
	return $array;
}


?>
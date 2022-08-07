<?php
error_reporting(E_ERROR | E_PARSE);
header("Content-Type:application/json");

$partidas = Select();


$resposta = [];
try{
	foreach($partidas as $partida){

	#Time mandante
	$id_mandante = $partida['clube_id_mandante'];
	if($resposta[$id_mandante] != null){
		$vitorias = $resposta[$id_mandante]['V'];
		$cartaoAmarelo = $resposta[$id_mandante]['CA'];
		$cartaoVermelho = $resposta[$id_mandante]['CV'];
        $gols = $resposta[$id_mandante]['TotalGols'];
	}else{	
        $gols = 0;
		$vitorias = 0;
		$cartaoAmarelo = 0;
		$cartaoVermelho = 0;
	}

    $derrotas = derrotaMandante($partida);
    $gols += $partida['gols_mandante'];
	$vitorias += vitoriaMandante($partida);
	$cartaoAmarelo = $partida['cartao_amarelo_mandante'];
	$cartaoVermelho = $partida['cartao_vermelho_mandante'];
	$escudo = $partida['escudo_mandante'];
    $nome =  $partida['nome_mandante'];

	$time_mandante = [
        'Nome'=> $nome,
        'D' =>$derrotas,
		'V'=> $vitorias,
        'TotalGols'=>$gols,
		'CA'=> $cartaoAmarelo,
		'CV'=>$cartaoVermelho,
		'Escudo'=>$escudo
	];

	$resposta[$id_mandante] = $time_mandante ;
	
	
	#Time Visitante
	$id_visitante = $partida['clube_id_visitante'];
	if($resposta[$id_visitante] != null){
		$vitorias = $resposta[$id_visitante]['V'];
		$cartaoAmarelo = $resposta[$id_visitante]['CA'];
		$cartaoVermelho = $resposta[$id_visitante]['CV'];
        $gols = $resposta[$id_visitante]['TotalGols'];
	}else{	
        $gols = 0;
		$vitorias = 0;
		$cartaoAmarelo = 0;
		$cartaoVermelho = 0;
	}

    $derrotas = derrotaVisitante($partida);
    $gols += $partida['gols_visitante'];
	$vitorias += vitoriaVisitante($partida);
	$cartaoAmarelo = $partida['cartao_amarelo_visitante'];
	$cartaoVermelho = $partida['cartao_vermelho_visitante'];
	$escudo = $partida['escudo_visitante'];
    $nome =  $partida['nome_visitante'];

	$time_visitante = [
        'Nome'=> $nome,
        'D' =>$derrotas,
		'V'=> $vitorias,
        'TotalGols'=>$gols,
		'CA'=> $cartaoAmarelo,
		'CV'=>$cartaoVermelho,
		'Escudo'=>$escudo
	];

	$resposta[$id_visitante] = $time_visitante ;
}
}catch(Exception $e){
	response(500,$e->getMessage());
}

response(200,"Times encontrados com sucesso",$resposta);


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
	$sql = 'SELECT disputa.clube_id_mandante, disputa.clube_id_visitante, disputa.cartao_vermelho_mandante, disputa.cartao_vermelho_visitante, disputa.cartao_amarelo_mandante, disputa.cartao_amarelo_visitante, disputa.gols_mandante, disputa.gols_visitante, time1.nome AS nome_mandante, time2.nome AS nome_visitante, time1.escudo as escudo_mandante, time2.escudo as escudo_visitante FROM `disputa` INNER JOIN time time1 ON time1.id_clube=disputa.clube_id_mandante INNER JOIN time time2 ON time2.id_clube=disputa.clube_id_visitante;';
	$stmt = $conn->prepare($sql);
	$stmt->execute();
	$stmt->setFetchMode(PDO::FETCH_ASSOC);

	foreach(new RecursiveArrayIterator($stmt->fetchAll()) as $k=>$row) {
	  array_push($array,$row);
	}
	return $array;
}


function derrotaMandante($partida){
	if($partida['gols_mandante'] > $partida['gols_visitante']){
		$vitoria = 1;
	}else{
		$vitoria = 0;
	}
	return $vitoria;
}
function derrotaVisitante($partida){
	if($partida['gols_visitante'] > $partida['gols_mandante']){
		$vitoria = 1;
	}else{
		$vitoria = 0;
	}
	return $vitoria;
}


function vitoriaMandante($partida){
	if($partida['gols_mandante'] > $partida['gols_visitante']){
		$vitoria = 1;
	}else{
		$vitoria = 0;
	}
	return $vitoria;
}
function vitoriaVisitante($partida){
	if($partida['gols_visitante'] > $partida['gols_mandante']){
		$vitoria = 1;
	}else{
		$vitoria = 0;
	}
	return $vitoria;
}
?>
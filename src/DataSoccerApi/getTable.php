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
		
		$pontos = $resposta[$id_mandante]['Pts'];
		$empates = $resposta[$id_mandante]['E'];
		$jogos = $resposta[$id_mandante]['J'];
		$vitorias = $resposta[$id_mandante]['V'];
		$golsPro = $resposta[$id_mandante]['GP'];
		$golsContra = $resposta[$id_mandante]['GC'];
		$saldoGols = $resposta[$id_mandante]['SG'];
		$cartaoAmarelo = $resposta[$id_mandante]['CA'];
		$cartaoVermelho = $resposta[$id_mandante]['CV'];
	}else{
		$pontos = 0;
		$empates = 0;
		$jogos = 0;
		$vitorias = 0;
		$golsPro = 0;
		$golsContra = 0;
		$saldoGols = 0;
		$cartaoAmarelo = 0;
		$cartaoVermelho = 0;
	}

	$pontos += pontosMandante($partida);
	$empates += empate($partida);
	$jogos++;
	$vitorias += vitoriaMandante($partida);
	$golsPro += $partida['gols_mandante'];
	$golsContra += $partida['gols_visitante'];
	$saldoGols += $partida['gols_mandante'];
	$cartaoAmarelo = $partida['cartao_amarelo_mandante'];
	$cartaoVermelho = $partida['cartao_vermelho_mandante'];
	$escudo = $partida['escudo_mandante'];
	$nome = $partida['nome_mandante'];
	$time_mandante = [
		'Pts'=> $pontos,
		'E' => $empates,
		'J'=> $jogos,
		'V'=> $vitorias,
		'GP'=>$golsPro,
		'GC'=>$golsContra,
		'SG'=>$saldoGols,
		'CA'=> $cartaoAmarelo,
		'CV'=>$cartaoVermelho,
		'Escudo'=>$escudo_mandante,
		'Nome' =>$nome
	];

	$resposta[$id_mandante] = $time_mandante ;
	
	
	#Time Visitante
	$id_visitante = $partida['clube_id_visitante'];
	if($resposta[$id_visitante ] != null){
	
		$pontos = $resposta[$id_visitante]['Pts'];
		$empates = $resposta[$id_visitante]['E'];
		$jogos = $resposta[$id_visitante]['J'];
		$vitorias = $resposta[$id_visitante]['V'];
		$golsPro = $resposta[$id_visitante]['GP'];
		$golsContra = $resposta[$id_visitante]['GC'];
		$saldoGols = $resposta[$id_visitante]['SG'];
		$cartaoAmarelo = $resposta[$id_visitante]['CA'];
		$cartaoVermelho = $resposta[$id_visitante]['CV'];
	}else{
		$pontos = 0;
		$empates = 0;
		$jogos = 0;
		$vitorias = 0;
		$golsPro = 0;
		$golsContra = 0;
		$saldoGols = 0;
		$cartaoAmarelo = 0;
		$cartaoVermelho = 0;
		
	}

	$pontos += pontosVisitante($partida);
	$empates += empate($partida);
	$jogos++;
	$vitorias += vitoriaVisitante($partida);
	$golsPro += $partida['gols_visitante'];
	$golsContra += $partida['gols_mandante'];
	$saldoGols += $partida['gols_visitante'];
	$cartaoAmarelo = $partida['cartao_amarelo_visitante'];
	$cartaoVermelho = $partida['cartao_vermelho_visitante'];
	$escudo = $partida['escudo_visitante'];
	$nome = $partida['nome_visitante'];
	$time_visitante= [
		'Pts'=> $pontos,
		'E' => $empates,
		'J'=> $jogos,
		'V'=> $vitorias,
		'GP'=>$golsPro,
		'GC'=>$golsContra,
		'SG'=>$saldoGols,
		'CA'=> $cartaoAmarelo,
		'CV'=>$cartaoVermelho,
		'Escudo'=> $escudo,
		'Nome' =>$nome
	];
	$resposta[$id_visitante] = $time_visitante ;
}
}catch(Exception $e){
	response(500,$e->getMessage());
}

response(200,"Tabela encontrada com sucesso",$resposta);


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

function pontosMandante($partida){
	if($partida['gols_mandante'] > $partida['gols_visitante']){
		$pontos = 3;
	}else if($partida['gols_mandante'] == $partida['gols_visitante']){
		$pontos = 1;
	}
	return $pontos;
}
function pontosVisitante($partida){
	if($partida['gols_visitante'] > $partida['gols_mandante']){
		$pontos = 3;
	}else if($partida['gols_visitante'] == $partida['gols_mandante']){
		$pontos = 1;
	}
	return $pontos;
}

function empate($partida){
	if($partida['gols_mandante'] == $partida['gols_visitante']){
		$empate = 1;
	}else{
		$empate = 0;
	}
	return $empate;
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

function vote_q(agent_uri,stance,bill_uri){
	return ' <' + agent_uri   + '> ' + ' <' + bill_uri 	 + '> ' + stance + ' .\n';
}

// this is filled up, and then sent as a single massive query when all data has been retrieved.
var rdf_triples = [];

// number of queries that have been sent but no response was received yet.
// used to decide when to send the single massive query
var num_queries_waited_for = 0;

function updateCounter(){
	document.getElementById('count').innerHTML = num_queries_waited_for;
}

function process_vote(agent_uri,stance,bill_uri){
	rdf_triples.push(vote_q(agent_uri,stance,bill_uri));
}


function interpret_stance(vote){
	var stance = vote.option;
	if (stance.key=='-'||stance.value=='Nay') return -1;
	else if (stance.key=='+'||stance.value=='Jay') return 1;
	else if (stance.key=='0'||stance.value=='Not Voting') return 0;

	console.log("unexpected stance values:",stance);
	return false;
}

function send_massive_query(){
	var q = "@prefix "+DB_NS + ": <" + PREFIX + ">.\n" + "@prefix "+GT_NS + ": <" + GT_PREFIX + ">.\n"

	for (var i in rdf_triples) {
		q += "\n" + rdf_triples[i];
	}

	console.log(q)
	document.getElementById('q').innerText = q;
	$.post('/store',data={'data': q}, function(d){
		document.getElementById('counter-container').innerHTML = "Server says: " + (JSON.stringify(d))
	});
}

function process_vote_(bill){

	var bill_uri = GT_NS + ':vote?id=' + bill.id;

	var votes_url = GT_PREFIX + 'vote_voter?vote='+bill.id;
	num_queries_waited_for++;
	updateCounter();
	$.getJSON({
		url: votes_url+"&limit=10",
		success:function(s){
			// for every vote, store a (politician (votesYes|votesNo|abstains) bill) tuple
			var votes = s.objects;
			for (var l in votes){
				var stance = interpret_stance(votes[l]);
				if (stance===false) continue;
				var agent_uri = GT_NS + ':person/' + votes[l].person.id;
				process_vote(agent_uri,stance,bill_uri);
			}
			num_queries_waited_for--;
			updateCounter()
		},
		datatype:'json'
	})
}

function import_data(){

	// get list of bills

	num_queries_waited_for++;
	updateCounter();
	$.getJSON({
		url:GT_PREFIX+"vote?limit=1000",
		success:function(d){

			var bills = d.objects;
			for (var i = 0; i < bills.length;i++) {

				process_vote_(bills[i]);
			}
			num_queries_waited_for--;
			updateCounter()
		},
		datatype:'json'
	});
	var interval = setInterval(function(){if (num_queries_waited_for==0) {
		clearInterval(interval);
		document.getElementById('counter-container').innerHTML = "Sending store query to db..."
		send_massive_query();
	}},250);
}

function init(){
	document.getElementById('counter-container').style.display='inline-block';
	document.getElementById('button').style.display='none';
	import_data();
}
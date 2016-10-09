
function bill_q(uri,stringified){
	return '<' + uri + '> a '+DB_NS+':Bill; '+DB_NS+':stringified \"' + stringified + "\"@en. ";
}

function agent_q(uri){
	return "<" + uri + '> a '+DB_NS+':Agent. ';
}

function vote_q(bill_uri,agent_uri,stance){

	return '[ a '+DB_NS+':Vote; '+DB_NS+':voter <' + agent_uri + '>; '+DB_NS+':bill <'+ bill_uri + '>; '+DB_NS+':stance '+ stance +' ] .';
}

// this is filled up, and then sent as a single massive query when all data has been retrieved.
var query_parts = [];

// number of queries that have been sent but no response was received yet.
// used to decide when to send the single massive query
var num_queries_waited_for = 0;

function updateCounter(){
	document.getElementById('count').innerHTML = num_queries_waited_for;
}

function process_bill(bill_uri, stringified){
	query_parts.push(bill_q(bill_uri,stringified.replace(/"/g, '\\"')));
}

function process_vote(bill_uri,agent_uri,stance){
	query_parts.push(vote_q(bill_uri,agent_uri,stance));
}

function process_agent(agent_uri){
	query_parts.push(agent_q(agent_uri));
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

	var uniqueArray = query_parts.filter(function(item, pos) {return query_parts.indexOf(item) == pos;});
	var q = PREFIX;
	for (var i in uniqueArray) q += uniqueArray[i];
	$.post('/store',data={'data': q}, console.log);
}

function import_data(){

	// get list of bills

	num_queries_waited_for++;
	updateCounter();
	$.getJSON({
		url:"https://www.govtrack.us/api/v2/vote",
		success:function(d){
			var bills = d.objects;
			for (var i = 0; i < bills.length;i++) {
				var bill_uri = "https://www.govtrack.us/api/v2/vote?id=" + bills[i].id;
				process_bill(bill_uri,bills[i].question);
				var votes_url = "https://www.govtrack.us/api/v2/vote_voter?vote="+bills[i].id;
				num_queries_waited_for++;
				updateCounter();
				$.getJSON({
					url: votes_url,
					success:function(s){
						// for every vote, store a (politician (votesYes|votesNo|abstains) bill) tuple
						var votes = s.objects;
						for (var l in votes){
							var stance = interpret_stance(votes[l]);
							if (stance===false) continue;
							var agent_uri = 'https://www.govtrack.us/api/v2/person/' + votes[l].person.id;
							process_agent(agent_uri);
							process_vote(bill_uri,agent_uri,stance);
						}
						num_queries_waited_for--;
						updateCounter()
					},
					datatype:'json'
				})
			}
			num_queries_waited_for--;
			updateCounter()
		},
		datatype:'json'
	});
	var interval = setInterval(function(){if (num_queries_waited_for==0) {clearInterval(interval);send_massive_query();}},250);
}

function init(){
	import_data();
	document.getElementById('counter-container').style.display='inline-block';	
}
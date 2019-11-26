$(document).ready(function() {
	var result = []

	function onmousemove(event) {
		if (!_.get(_.last(result), 'move')) {
			result.push({move: []})
		}

		_.last(result).move.push([event.clientX, event.clientY])
	}

	function onclick(event) {
		result.push({'action': event.type})
		console.log(event)
	}

	document.addEventListener('keyup', function(event) {
		if (event.keyCode === 27) {
		console.log(result)
		document.removeEventListener('mousemove', onmousemove)
		document.removeEventListener('click', onclick)
	}
})

//removeEventListener
	document.addEventListener('mousemove', onmousemove)
	document.addEventListener('click', onclick)
}
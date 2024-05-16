$(document).ready(function() {
    const cueBall = $('#cue-ball');
    let isDragging = false;
    let currentLine = null;

    makePlayerNames();
    $(document).mousemove(changeCursorCoords);

    cueBall.on('mousedown', startDrawing);
    $(document).on('mousemove', makeLine);
    $(document).on('mouseup', endDrawing);

    function makePlayerNames() {
        const player1Name = localStorage.getItem("player1") || "PLAYER 1";
        const player2Name = localStorage.getItem("player2") || "PLAYER 2";
        $("#player").text(`PLAYER 1: ${player1Name} | PLAYER 2: ${player2Name}`);
    }

    function changeCursorCoords(event) {
        $('#valx, #valy').remove(); // Remove previous values
        const { pageX: x, pageY: y } = event;
        $("<div>").attr("id", "valx").text(x).appendTo("#x");
        $("<div>").attr("id", "valy").text(y).appendTo("#y");
    }

    function startDrawing(e) {
        e.preventDefault();
        const svg = $(this).closest('svg').get(0);
        const point = getSVGCoordinates(svg, e.clientX, e.clientY);
        currentLine = createLine(point.x, point.y, point.x, point.y).appendTo(svg);
        isDragging = true;
    }

    function makeLine(e) {
        if (!isDragging || !currentLine) return;
        const svg = cueBall.closest('svg').get(0);
        const point = getSVGCoordinates(svg, e.clientX, e.clientY);
        currentLine.attr({ x2: point.x, y2: point.y });
    }

    function endDrawing(e) {
        if (!isDragging || !currentLine) return;
        isDragging = false;
        const svg = cueBall.closest('svg').get(0);
        const point = getSVGCoordinates(svg, e.clientX, e.clientY);
        sendLineData(currentLine.attr('x1'), currentLine.attr('y1'), point.x, point.y);
        currentLine.remove();
        currentLine = null; 
    }

    function getSVGCoordinates(svg, x, y) {
        const pt = svg.createSVGPoint();
        pt.x = x; pt.y = y;
        return pt.matrixTransform(svg.getScreenCTM().inverse());
    }

    function sendLineData(x1, y1, x2, y2) {
        $.ajax({
            type: "POST",
            url: "/send-data", // Server endpoint
            data: JSON.stringify({ x1, y1, x2, y2 }),
            contentType: "application/json",
            success: function(){
                console.log("Data sent successfully");
                createSVGanimation();
            },
            error: () => console.log("Error sending data")
        });
    }

    function createLine(x1, y1, x2, y2) {
        return $(document.createElementNS('http://www.w3.org/2000/svg', 'line'))
            .attr({ x1, y1, x2, y2, stroke: 'black', 'stroke-width': '15' });
    }

    let svgIndex = 0;
    function createSVGanimation() {
        $("#pool-table").load(`/table-${svgIndex}.svg`, function(response, status, xhr) {
            if (status == "error") {
                console.log("No more SVG files to load or encountered an error.");
                return;
            }
            svgIndex++;
            setTimeout(createSVGanimation, 10); //10 millisecond      
        });
    }
});


// Trigger update

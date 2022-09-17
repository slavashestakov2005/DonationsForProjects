function textInput(document, textarea){
    textarea.style.height = '1px';
    textarea.style.height = (textarea.scrollHeight + 6) + 'px';
}

function listenInput(document){
    let areas = document.getElementsByClassName('textarea');
    for (let textarea of areas){
        textarea.oninput = function(){ textInput(document, textarea); };
        textInput(document, textarea);
    }
}

function box_click(box){
    let children = box.children();
    let chb = $(children[0]).children()[0];
    if (chb.checked){
        children[1].style.display = 'block';
        children[2].style.display = 'none';
    } else{
        children[1].style.display = 'none';
        children[2].style.display = 'block';
    }
}

function listenCheckbox(document){
    let boxes = document.getElementsByClassName('chekable');
    for(let box of boxes){
        box = $(box);
        $(box.children()[0]).children()[0].onclick = function(){ box_click(box); };
        box_click(box);
    }
}

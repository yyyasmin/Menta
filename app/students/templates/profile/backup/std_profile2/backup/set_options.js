// FROM https://stackoverflow.com/questions/2738254/javascript-innerhtml-not-working-with-html-select-menus -->

while ( sub_tag_select.childNodes.length >= 1 )   {
    sub_tag_select.removeChild(sub_tag_select.firstChild);       
}

for(let sub_tag of data.sub_tags)  {
    newOption = document.createElement('option');
    newOption.value=sub_tag.id;
    newOption.text=sub_tag.title;
    sub_tag_select.appendChild(newOption);
}
function getPartialDOM(target, levels = 1) {

  let current = target.cloneNode(true);  

  for (let i = 0; i < levels; i++) {
    let original = target;                  
    let parent = original.parentElement;    
    if (!parent) break;

    let prev = original.previousElementSibling;
    let next = original.nextElementSibling;

    
    let partialParent = parent.cloneNode(false);

    if (prev) partialParent.appendChild(prev.cloneNode(false));  
    partialParent.appendChild(current);                          
    if (next) partialParent.appendChild(next.cloneNode(false));  

    
    target = parent;        
    current = partialParent; 
  }

  return current;
}

// Example usage
document.addEventListener("click", function (event) {
  let partialDOM = getPartialDOM(event.target, 2); 
  console.log(partialDOM.outerHTML);
  console.log(event.target.outerHTML);
});





// from lxml import html, etree

// def get_partial_dom(target, levels=1):
//     current = etree.Element(target.tag, **target.attrib)
//     current.text = target.text

//     for i in range(levels):
//         parent = target.getparent()
//         if parent is None:
//             break

//         # Clone parent without children
//         partial_parent = etree.Element(parent.tag, **parent.attrib)

//         # Add prev sibling
//         prev = target.getprevious()
//         if prev is not None:
//             partial_parent.append(etree.Element(prev.tag, **prev.attrib))

//         # Add current
//         partial_parent.append(current)

//         # Add next sibling
//         nxt = target.getnext()
//         if nxt is not None:
//             partial_parent.append(etree.Element(nxt.tag, **nxt.attrib))

//         # Update loop vars
//         target = parent
//         current = partial_parent

//     return current
$(document).ready(function() {
  var el = document.getElementById("markdown");
  if (el) {
    new SimpleMDE({
      element: el,
      spellChecker: false,
      placeholder: "Use Markdown for your **writeup**:\n\n```python\nfrom pwn import *\n\ndef exploit():\n  pass\n```"
    });
  }
});

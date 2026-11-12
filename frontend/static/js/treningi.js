// Stran Treningi: vrstice serij odkriva »+ Dodaj serijo«, starejše treninge »Naloži starejše …«.
// shortcut: največ 9 vrstic serij (toliko jih pripravi backend); za več vrstic ali skupine po vajah je potreben backend.
(function () {
  function postopno(elementi, gumb, vidnih, korak) {
    if (!gumb || elementi.length <= vidnih) return;
    elementi.slice(vidnih).forEach((e) => (e.hidden = true));
    gumb.hidden = false;
    gumb.addEventListener("click", () => {
      elementi.filter((e) => e.hidden).slice(0, korak).forEach((e) => (e.hidden = false));
      gumb.hidden = !elementi.some((e) => e.hidden);
    });
  }
  const vrstice = [...document.querySelectorAll("#serije tr.serija")];
  const polna = (tr) => [...tr.querySelectorAll("select, input:not([type=checkbox])")].some((p) => p.value);
  // Vidne ostanejo vse izpolnjene vrstice in ena prazna za njimi, najmanj tri.
  postopno(vrstice, document.getElementById("dodaj-serijo"), Math.max(vrstice.map(polna).lastIndexOf(true) + 2, 3), 1);
  postopno([...document.querySelectorAll(".pretekli .trening")], document.getElementById("nalozi-starejse"), 5, 5);
})();

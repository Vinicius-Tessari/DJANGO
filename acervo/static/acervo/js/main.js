const els = Array.from(document.querySelectorAll('.reveal'));
const onIntersect = (entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting){
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
};
const io = new IntersectionObserver(onIntersect, { threshold: 0.12 });
els.forEach(el => io.observe(el));

document.addEventListener("DOMContentLoaded", () => {
  const emblaNode = document.getElementById("embla")
  if (!emblaNode) return

  const embla = EmblaCarousel(emblaNode, { loop: true })
  const thumbs = document.querySelectorAll("#thumbs [data-index]")

  thumbs.forEach(el => {
    el.addEventListener("click", () => embla.scrollTo(+el.dataset.index))
  })

  const updateThumbs = () => {
    const active = embla.selectedScrollSnap()
    thumbs.forEach(el => {
      const isActive = +el.dataset.index === active
      el.classList.toggle("border-base-300", isActive)
      el.classList.toggle("border-transparent", !isActive)
    })
  }

  embla.on("select", updateThumbs)
  updateThumbs()
})

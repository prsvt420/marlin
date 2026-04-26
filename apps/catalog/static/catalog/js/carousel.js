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
      el.classList.toggle("border-edge", isActive)
      el.classList.toggle("border-transparent", !isActive)
    })
  }

  embla.on("select", updateThumbs)
  updateThumbs()
})

document.addEventListener("DOMContentLoaded", () => {
  const similarNode = document.getElementById("similar-embla")
  if (!similarNode) return

  EmblaCarousel(similarNode, { dragFree: true, loop: false, align: "start" })
})

document.addEventListener("DOMContentLoaded", () => {
  const popularNode = document.getElementById("popular-embla")
  if (!popularNode) return

  EmblaCarousel(popularNode, { dragFree: true, loop: false, align: "start" })
})

document.addEventListener("DOMContentLoaded", () => {
  const newNode = document.getElementById("new-embla")
  if (!newNode) return

  EmblaCarousel(newNode, { dragFree: true, loop: false, align: "start" })
})

import preloader_styles from './styles/index.scss'
const WRAPPER_CLASS = 'preloader'
const CONTENT_CLASS = 'preloader__content'

function wait(delay = 200) {
  return new Promise((resolve) => {
    setTimeout(() => {
      return resolve()
    }, delay)
  })
}

class AppPreloader extends HTMLElement {
  constructor() {
    super()
    this._initialize()
  }
  _create_wrapper() {
    const wrapper = document.createElement('div')
    wrapper.classList.add(WRAPPER_CLASS)
    if (this.hasAttribute('default-active')) {
      wrapper.classList.add(`${WRAPPER_CLASS}-active`)
    }

    return wrapper
  }
  _create_progress_bar() {
    const progress_bar = document.createElement('div')
    const progress_el = document.createElement('div')
    const progress_circle = document.createElement('div')
    const progress_spin = document.createElement('div')

    progress_bar.classList.add('loader')
    progress_el.classList.add('loader__element')
    progress_circle.classList.add('loader__circle')
    progress_spin.classList.add('loader__spin')

    progress_bar.appendChild(progress_el)
    progress_el.appendChild(progress_circle)
    for (let i = 0; i <= 9; i++) {
      progress_el.appendChild(progress_spin.cloneNode())
    }
    return progress_bar
  }
  _create_text() {
    const p = document.createElement('p')
    const span = document.createElement('span')
    const span_welcome = document.createElement('span')
    const wrapper = document.createElement('div')

    span.textContent = 'Добро пожаловать в '
    span_welcome.textContent = 'Smetaverse!'

    p.classList.add('preloader__text')
    wrapper.classList.add('loader__wrapper')
    span.classList.add('preloader__text-span')

    p.appendChild(span)
    span.insertAdjacentElement('afterend', span_welcome)
    wrapper.appendChild(p)

    return wrapper
  }
  _create_content() {
    const content = document.createElement('div')
    content.classList.add(CONTENT_CLASS)
    const progress_bar = this._create_progress_bar()
    const welcome_text = this._create_text()
    content.appendChild(welcome_text)
    welcome_text.appendChild(progress_bar)
    return content
  }
  _create_styles() {
    const styles = document.createElement('style')
    styles.textContent = preloader_styles
    return styles
  }
  _hook() {
    window.preloader = {
      show: this.show.bind(this),
      hide: this.hide.bind(this),
      preload_images: this.preload_images.bind(this),
    }
  }
  show() {
    const wrapper = this.shadowRoot.querySelector(`.${WRAPPER_CLASS}`)
    wrapper.classList.add(`${WRAPPER_CLASS}-active`)
  }
  hide() {
    const wrapper = this.shadowRoot.querySelector(`.${WRAPPER_CLASS}`)
    wrapper.classList.remove(`${WRAPPER_CLASS}-active`)
  }
  get is_active() {
    const wrapper = this.shadowRoot.querySelector(`.${WRAPPER_CLASS}`)
    return wrapper.classList.contains(`${WRAPPER_CLASS}-active`)
  }
  async preload_images() {
    this.show()
    const all_images = document.querySelectorAll('img')
    const all_videos = document.querySelectorAll('video')
    const all_media = [...all_images, ...all_videos]
    let total_media = all_media.length
    let total_media_loaded = 0
    const handler = async () => {
      total_media_loaded++
      const current_loading_progress = (total_media_loaded / total_media) * 100
      if (current_loading_progress > 80) {
        await wait(1000)
        this.hide()
      }
    }
    if (total_media < 10) {
      await wait(1000)
      this.hide()
    }
    all_media.forEach((media) => {
      media.onload = handler
      media.onloadeddata = handler
      media.onerror = handler
    })
  }
  _initialize() {
    this._hook()

    const shadow = this.attachShadow({ mode: 'open' })
    const styles = this._create_styles()
    const wrapper = this._create_wrapper()
    const content = this._create_content()
    setTimeout(() => {
      content
        .querySelector('.preloader__text')
        .classList.add('preloader__text--active')
    }, 10)

    setTimeout(() => {
      content
        .querySelector('.loader__wrapper')
        .classList.add('loader__wrapper--scrolled')
      content
        .querySelector('.preloader__text-span')
        .classList.add('preloader__text-span--hidden')
    }, 800)

    shadow.appendChild(styles)
    shadow.appendChild(wrapper)
    wrapper.appendChild(content)
    window.addEventListener('DOMContentLoaded', () => {
      const preload_media = this.hasAttribute('preload-media')
      preload_media ? this.preload_images() : this.hide()
    })
  }
}

export function define() {
  customElements.define('app-preloader', AppPreloader)
}

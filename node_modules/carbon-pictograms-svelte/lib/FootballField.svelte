<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M31,5.64H1C0.801,5.64,0.64,5.801,0.64,6v20	c0,0.199,0.161,0.36,0.36,0.36h30c0.199,0,0.36-0.161,0.36-0.36V6C31.36,5.801,31.199,5.64,31,5.64z M25.64,12.64H24v0.72h1.64v5.28	H24v0.721h1.64v6.279h-4.28v-6.28H23v-0.72h-1.64v-5.28H23v-0.72h-1.64V6.36h4.279L25.64,12.64L25.64,12.64z M6.36,19.36H8v-0.72	H6.36v-5.28H8v-0.72H6.36V6.36h4.28v6.28H9v0.72h1.64v5.28H9v0.721h1.64v6.279H6.36V19.36z M11.36,19.36H13v-0.72h-1.64v-5.28H13	v-0.72h-1.64V6.36h4.28v6.28H14v0.72h1.64v5.28H14v0.721h1.64v6.279h-4.28C11.36,25.64,11.36,19.36,11.36,19.36z M16.36,19.36H18	v-0.72h-1.64v-5.28H18v-0.72h-1.64V6.36h4.28v6.28H19v0.72h1.64v5.28H19v0.721h1.64v6.279h-4.28	C16.36,25.64,16.36,19.36,16.36,19.36z M1.36,19.36H3v-0.72H1.36v-5.28H3v-0.72H1.36V6.36h4.28v19.28H1.36V19.36z M26.36,25.64V6.36	h4.279v6.28H29v0.72h1.64v5.28H29v0.721h1.64v6.279C30.64,25.64,26.36,25.64,26.36,25.64z M9.5,8.36h-2V7.64h2V8.36z M9.5,23.64	v0.721h-2V23.64H9.5z M14.5,8.36h-2V7.64h2V8.36z M14.5,23.64v0.721h-2V23.64H14.5z M19.5,8.36h-2V7.64h2V8.36z M19.5,23.64v0.721	h-2V23.64H19.5z M22.5,8.36V7.64h2v0.72H22.5z M22.5,23.64h2v0.721h-2V23.64z M23.64,15h0.721v2H23.64V15z M8.36,17H7.64v-2h0.72V17	z"></path>
</svg>
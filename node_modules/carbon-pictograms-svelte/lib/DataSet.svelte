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
  <path d="M28,31.36H4c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h18	c0.096,0,0.188,0.038,0.255,0.105l6,6C28.322,6.813,28.36,6.904,28.36,7v24C28.36,31.199,28.199,31.36,28,31.36z M4.36,30.64h23.28	V7.36H22c-0.199,0-0.36-0.161-0.36-0.36V1.36H4.36V30.64z M22.36,6.64h4.771L22.36,1.869V6.64z M25,27.36H7	c-0.199,0-0.36-0.161-0.36-0.36V11c0-0.199,0.161-0.36,0.36-0.36h18c0.199,0,0.36,0.161,0.36,0.36v16	C25.36,27.199,25.199,27.36,25,27.36z M19.36,26.64h5.279v-3.28H19.36V26.64z M13.36,26.64h5.28v-3.28h-5.28	C13.36,23.36,13.36,26.64,13.36,26.64z M7.36,26.64h5.28v-3.28H7.36V26.64z M19.36,22.64h5.279v-3.28H19.36V22.64z M13.36,22.64	h5.28v-3.28h-5.28C13.36,19.36,13.36,22.64,13.36,22.64z M7.36,22.64h5.28v-3.28H7.36V22.64z M19.36,18.64h5.279v-3.28H19.36V18.64z M13.36,18.64h5.28v-3.28h-5.28C13.36,15.36,13.36,18.64,13.36,18.64z M7.36,18.64h5.28v-3.28H7.36V18.64z M19.36,14.64h5.279v-3.28	H19.36V14.64z M13.36,14.64h5.28v-3.28h-5.28C13.36,11.36,13.36,14.64,13.36,14.64z M7.36,14.64h5.28v-3.28H7.36V14.64z"></path>
</svg>
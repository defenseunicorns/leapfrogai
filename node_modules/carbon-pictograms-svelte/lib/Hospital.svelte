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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V8c0-0.199,0.161-0.36,0.36-0.36h21.64V1	c0-0.199,0.161-0.36,0.36-0.36h8c0.199,0,0.36,0.161,0.36,0.36v30C31.36,31.199,31.199,31.36,31,31.36z M16.36,30.64h14.28V1.36	h-7.28V8c0,0.199-0.161,0.36-0.36,0.36H1.36v22.28h8.78V24c0-0.199,0.161-0.36,0.36-0.36H16c0.199,0,0.36,0.161,0.36,0.36V30.64z M10.86,30.64h4.78v-6.28h-4.78C10.86,24.36,10.86,30.64,10.86,30.64z M27.36,25h-0.72v-2h0.721L27.36,25L27.36,25z M21.86,25h-0.72	v-2h0.721L21.86,25L21.86,25z M5.36,25H4.64v-2h0.72C5.36,23,5.36,25,5.36,25z M27.36,21h-0.72v-2h0.721L27.36,21L27.36,21z M21.86,21h-0.72v-2h0.721L21.86,21L21.86,21z M16.36,21h-0.72v-2h0.72V21z M10.86,21h-0.72v-2h0.72V21z M5.36,21H4.64v-2h0.72	C5.36,19,5.36,21,5.36,21z M27.36,17h-0.72v-2h0.721L27.36,17L27.36,17z M21.86,17h-0.72v-2h0.721L21.86,17L21.86,17z M16.36,17	h-0.72v-2h0.72V17z M10.86,17h-0.72v-2h0.72V17z M5.36,17H4.64v-2h0.72C5.36,15,5.36,17,5.36,17z M27.36,13h-0.72v-2h0.721L27.36,13	L27.36,13z M21.86,13h-0.72v-2h0.721L21.86,13L21.86,13z M16.36,13h-0.72v-2h0.72V13z M10.86,13h-0.72v-2h0.72V13z M5.36,13H4.64v-2	h0.72C5.36,11,5.36,13,5.36,13z M27.36,6.5h-0.72V4.86H25V4.14h1.64V2.5h0.721v1.64H29v0.72h-1.64V6.5z"></path>
</svg>
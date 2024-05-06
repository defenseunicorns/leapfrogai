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
  <circle cx="13.5" cy="4" r=".5"></circle><circle cx="13.5" cy="11" r=".5"></circle><circle cx="27.5" cy="20" r=".5"></circle><circle cx="27.5" cy="27" r=".5"></circle><path d="M16,7.36H2C1.801,7.36,1.64,7.199,1.64,7V2c0-0.199,0.161-0.36,0.36-0.36h14c0.199,0,0.36,0.161,0.36,0.36v5 C16.36,7.199,16.199,7.36,16,7.36z M2.36,6.64h13.28V2.36H2.36V6.64z M10,3.64H4v0.72h6V3.64z M16,14.36H2 c-0.199,0-0.36-0.161-0.36-0.36V9c0-0.199,0.161-0.36,0.36-0.36h14c0.199,0,0.36,0.161,0.36,0.36v5 C16.36,14.199,16.199,14.36,16,14.36z M2.36,13.64h13.28V9.36H2.36V13.64z M10,10.64H4v0.72h6V10.64z M30,23.36H16 c-0.199,0-0.36-0.161-0.36-0.36v-5c0-0.199,0.161-0.36,0.36-0.36h14c0.199,0,0.36,0.161,0.36,0.36v5 C30.36,23.199,30.199,23.36,30,23.36z M16.36,22.64h13.28v-4.28H16.36V22.64z M24,19.64h-6v0.721h6V19.64z M30,30.36H16 c-0.199,0-0.36-0.161-0.36-0.36v-5c0-0.199,0.161-0.36,0.36-0.36h14c0.199,0,0.36,0.161,0.36,0.36v5 C30.36,30.199,30.199,30.36,30,30.36z M16.36,29.64h13.28v-4.28H16.36V29.64z M24,26.64h-6v0.721h6V26.64z M28.36,8 c0-0.199-0.161-0.36-0.36-0.36H18v0.72h9.64V16h0.721L28.36,8L28.36,8z M14,23.64H4.36V16H3.64v8c0,0.199,0.161,0.36,0.36,0.36h10 V23.64z"></path>
</svg>
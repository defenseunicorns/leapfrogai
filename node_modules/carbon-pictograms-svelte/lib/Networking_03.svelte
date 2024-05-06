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
  <path d="M31,31.36h-6c-0.199,0-0.36-0.161-0.36-0.36v-6c0-0.199,0.161-0.36,0.36-0.36h6	c0.199,0,0.36,0.161,0.36,0.36v6C31.36,31.199,31.199,31.36,31,31.36z M25.36,30.64h5.279v-5.28H25.36V30.64z M22,28.36H7	c-3.507,0-6.36-2.853-6.36-6.359c0-3.508,2.853-6.361,6.36-6.361h3v0.72H7c-3.11,0-5.64,2.531-5.64,5.641	c0,3.109,2.53,5.639,5.64,5.639h15V28.36z M19,19.36h-6c-0.199,0-0.36-0.161-0.36-0.36v-6c0-0.199,0.161-0.36,0.36-0.36h6	c0.199,0,0.36,0.161,0.36,0.36v6C19.36,19.199,19.199,19.36,19,19.36z M13.36,18.64h5.28v-5.28h-5.28	C13.36,13.36,13.36,18.64,13.36,18.64z M25,16.36h-3v-0.72h3c3.11,0,5.64-2.53,5.64-5.641c0-3.11-2.529-5.64-5.64-5.64H10V3.64h15	c3.507,0,6.36,2.853,6.36,6.359C31.36,13.507,28.507,16.36,25,16.36z M7,7.36H1C0.801,7.36,0.64,7.199,0.64,7V1	c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v6C7.36,7.199,7.199,7.36,7,7.36z M1.36,6.64h5.28V1.36H1.36V6.64z"></path>
</svg>
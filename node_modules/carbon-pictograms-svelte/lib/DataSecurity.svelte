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
  <path d="M17,26.36H1c-0.199,0-0.36-0.161-0.36-0.36v-7c0-0.199,0.161-0.36,0.36-0.36h16v0.721H1.36v6.279H17	V26.36z M17,17.36H1c-0.199,0-0.36-0.161-0.36-0.36v-7c0-0.199,0.161-0.36,0.36-0.36h25c0.199,0,0.36,0.161,0.36,0.36v3h-0.72v-2.64	H1.36v6.28H17V17.36z M26,8.36H1C0.801,8.36,0.64,8.199,0.64,8V1c0-0.199,0.161-0.36,0.36-0.36h25c0.199,0,0.36,0.161,0.36,0.36v7	C26.36,8.199,26.199,8.36,26,8.36z M1.36,7.64h24.28V1.36H1.36V7.64z M22,14.5c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1	S22.552,14.5,22,14.5z M23,4.5c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1S23,5.052,23,4.5z M25,31.36	c-3.507,0-6.36-2.854-6.36-6.36v-7.223l6.36-3.18l6.36,3.18V25C31.36,28.507,28.507,31.36,25,31.36z M19.36,18.223V25	c0,3.11,2.529,5.64,5.64,5.64s5.64-2.529,5.64-5.64v-6.777L25,15.402L19.36,18.223z"></path>
</svg>
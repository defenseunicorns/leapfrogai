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
  <path d="M15,15.36H9c-0.199,0-0.36-0.161-0.36-0.36V9	c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v6C15.36,15.199,15.199,15.36,15,15.36z M9.36,14.64h5.28V9.36H9.36	V14.64z M15.36,23v-6c0-0.199-0.161-0.36-0.36-0.36H9v0.72h5.64v5.279H9v0.721h6C15.199,23.36,15.36,23.199,15.36,23z M23.36,9	c0-0.199-0.161-0.36-0.36-0.36h-6v0.72h5.64V15h0.721L23.36,9L23.36,9z M16,31.36c-4.529,0-8.716-1.933-11.64-5.338V29H3.64v-4.36H8	v0.721H4.743C7.536,28.725,11.598,30.64,16,30.64c8.072,0,14.64-6.567,14.64-14.64h0.721C31.36,24.47,24.47,31.36,16,31.36z M1.36,16H0.64C0.64,7.53,7.53,0.64,16,0.64c4.529,0,8.716,1.933,11.64,5.337V3h0.721v4.36H24V6.64h3.257	C24.464,3.275,20.401,1.36,16,1.36C7.927,1.36,1.36,7.927,1.36,16z M23,23.36h-6c-0.199,0-0.36-0.161-0.36-0.36v-6	c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v6C23.36,23.199,23.199,23.36,23,23.36z M17.36,22.64h5.279v-5.28	H17.36V22.64z"></path>
</svg>
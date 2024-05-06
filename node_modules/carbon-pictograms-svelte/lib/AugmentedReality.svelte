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
  <path d="M22,31.36H4c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h18	c0.199,0,0.36,0.161,0.36,0.36v2.791l6.818,3.896C29.291,7.751,29.36,7.871,29.36,8v8c0,0.129-0.069,0.249-0.182,0.312l-6.818,3.896	V31C22.36,31.199,22.199,31.36,22,31.36z M4.36,30.64h17.28v-6.28H4.36V30.64z M4.36,23.64h17.28v-3.431l-6.818-3.896	C14.709,16.249,14.64,16.129,14.64,16V8c0-0.129,0.069-0.249,0.181-0.312l6.818-3.896V1.36H4.36V23.64z M22.36,12.209v7.171	l6.279-3.589V8.62L22.36,12.209z M15.36,15.791l6.28,3.589v-7.171L15.36,8.62V15.791z M15.726,8L22,11.585L28.274,8L22,4.415	L15.726,8z M14,27.5c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1S14,28.052,14,27.5z"></path>
</svg>
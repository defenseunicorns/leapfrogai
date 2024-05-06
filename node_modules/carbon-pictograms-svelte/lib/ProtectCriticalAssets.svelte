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
  <path d="M17,28.36H1	c-0.199,0-0.36-0.161-0.36-0.36V7c0-0.096,0.038-0.187,0.105-0.254l6-6C6.813,0.678,6.904,0.64,7,0.64h15	c0.199,0,0.36,0.161,0.36,0.36v12h-0.72V1.36H7.36V7c0,0.199-0.161,0.36-0.36,0.36H1.36v20.28H17V28.36z M1.869,6.64H6.64V1.869	L1.869,6.64z M16.5,22.36H4v-0.72h12.5V22.36z M16.5,19.36H4v-0.72h12.5V19.36z M16.5,16.36H4v-0.72h12.5V16.36z M19,13.36H4v-0.72	h15V13.36z M25,31.36c-3.507,0-6.36-2.854-6.36-6.36v-7.223l6.36-3.18l6.36,3.18V25C31.36,28.507,28.507,31.36,25,31.36z M19.36,18.223V25c0,3.11,2.529,5.64,5.64,5.64s5.64-2.529,5.64-5.64v-6.777L25,15.402L19.36,18.223z"></path>
</svg>
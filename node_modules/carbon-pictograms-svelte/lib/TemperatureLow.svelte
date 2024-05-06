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
  <path d="M16,31.36c-3.507,0-6.36-2.854-6.36-6.36c0-2.601,1.597-4.939,4-5.9V1	c0-0.199,0.161-0.36,0.36-0.36h4c0.199,0,0.36,0.161,0.36,0.36v18.1c2.402,0.961,4,3.3,4,5.9C22.36,28.507,19.507,31.36,16,31.36z M14.36,12.36v6.989c0,0.152-0.096,0.288-0.24,0.34c-2.249,0.796-3.76,2.93-3.76,5.312c0,3.11,2.53,5.64,5.64,5.64	s5.64-2.529,5.64-5.64c0-2.382-1.511-4.516-3.76-5.312c-0.144-0.052-0.24-0.188-0.24-0.34V12.36H14.36z M14.36,11.64h3.28V1.36	h-3.28V11.64z M26,18.36h-4v-0.72h4V18.36z M30,15.36h-8v-0.72h8V15.36z M26,12.36h-4v-0.72h4V12.36z M30,9.36h-8V8.64h8V9.36z M26,6.36h-4V5.64h4V6.36z M30,3.36h-8V2.64h8V3.36z"></path>
</svg>
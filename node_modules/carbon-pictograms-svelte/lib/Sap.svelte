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
  <path d="M8,25.36c-0.625,0-1.153-0.425-1.312-1H1	c-0.199,0-0.36-0.161-0.36-0.36V8c0-0.199,0.161-0.36,0.36-0.36h18.688c0.158-0.576,0.687-1,1.312-1s1.153,0.424,1.312,1H31	c0.139,0,0.266,0.08,0.325,0.205s0.042,0.274-0.046,0.382l-13,16C18.211,24.312,18.108,24.36,18,24.36H9.312	C9.153,24.936,8.625,25.36,8,25.36z M8,23.36c-0.353,0-0.64,0.287-0.64,0.64S7.647,24.64,8,24.64c0.353,0,0.64-0.287,0.64-0.64	S8.353,23.36,8,23.36z M9.312,23.64h8.518L30.244,8.36h-7.933c-0.158,0.576-0.687,1-1.312,1s-1.153-0.424-1.312-1H1.36v15.28h5.329	c0.158-0.575,0.686-1,1.312-1S9.153,23.064,9.312,23.64z M21,7.36c-0.353,0-0.64,0.287-0.64,0.64S20.647,8.64,21,8.64	S21.64,8.353,21.64,8S21.353,7.36,21,7.36z"></path>
</svg>


describe("the files upload form action", () => {
    it("returns file objects on success", () => {
        const request = new Request('http://localhost:5173/chat/file-management', {
            method: 'POST',
            body: formData
        });
    })
})
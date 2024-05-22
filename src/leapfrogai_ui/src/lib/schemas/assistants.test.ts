import { ValidationError } from 'yup';
import { editAssistantInputSchema, supabaseAssistantInputSchema } from '$schemas/assistants';
import { ASSISTANTS_NAME_MAX_LENGTH } from '$constants';

describe('supabaseAssistantInputSchema', () => {
  it('should validate a correct input', async () => {
    const validInput = {
      name: 'Assistant Name',
      description: 'This is a description',
      instructions: 'These are instructions',
      temperature: 0.5,
      data_sources: 'some_data_source',
      avatar: 'avatar_url',
      avatarFile: null,
      pictogram: 'pictogram_url'
    };

    await expect(supabaseAssistantInputSchema.validate(validInput)).resolves.toBe(validInput);
  });

  it('should fail validation with missing required fields', async () => {
    // missing name
    const invalidInput = {
      description: 'This is a description',
      instructions: 'These are instructions',
      temperature: 0.5,
      data_sources: 'some_data_source',
      avatar: 'avatar_url',
      avatarFile: null,
      pictogram: 'pictogram_url'
    };

    await expect(supabaseAssistantInputSchema.validate(invalidInput)).rejects.toThrow(
      ValidationError
    );
  });

  it('should fail validation if name exceeds max length', async () => {
    const invalidInput = {
      name: 'a'.repeat(ASSISTANTS_NAME_MAX_LENGTH + 1),
      description: 'This is a description',
      instructions: 'These are instructions',
      temperature: 0.5,
      data_sources: 'some_data_source',
      avatar: 'avatar_url',
      avatarFile: null,
      pictogram: 'pictogram_url'
    };

    await expect(supabaseAssistantInputSchema.validate(invalidInput)).rejects.toThrow(
      ValidationError
    );
  });

  it('should fail validation if avatarFile is of incorrect type', async () => {
    const invalidFile = new File([''], 'avatar.gif', { type: 'image/gif' });
    const invalidInput = {
      name: 'Assistant Name',
      description: 'This is a description',
      instructions: 'These are instructions',
      temperature: 0.5,
      data_sources: 'some_data_source',
      avatar: 'avatar_url',
      avatarFile: invalidFile,
      pictogram: 'pictogram_url'
    };

    await expect(supabaseAssistantInputSchema.validate(invalidInput)).rejects.toThrow(
      ValidationError
    );
  });
});

describe('editAssistantInputSchema', () => {
  it('should validate a correct input', async () => {
    const validInput = {
      id: 'some-id',
      name: 'Assistant Name',
      description: 'This is a description',
      instructions: 'These are instructions',
      temperature: 0.5,
      data_sources: 'some_data_source',
      avatar: 'avatar_url',
      avatarFile: null,
      pictogram: 'pictogram_url'
    };

    await expect(editAssistantInputSchema.validate(validInput)).resolves.toBe(validInput);
  });

  it('should fail validation if id is missing', async () => {
    const invalidInput = {
      name: 'Assistant Name',
      description: 'This is a description',
      instructions: 'These are instructions',
      temperature: 0.5,
      data_sources: 'some_data_source',
      avatar: 'avatar_url',
      avatarFile: null,
      pictogram: 'pictogram_url'
    };

    await expect(editAssistantInputSchema.validate(invalidInput)).rejects.toThrow(ValidationError);
  });
});

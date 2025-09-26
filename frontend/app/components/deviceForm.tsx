import { FormProvider } from 'react-hook-form'
import type { FieldValues, UseFormReturn, SubmitHandler } from 'react-hook-form'

interface IFormProps<TFormValue extends FieldValues> {
  methods: UseFormReturn<TFormValue, any, TFormValue>,
  children: React.ReactNode,
  submitHandler: SubmitHandler<TFormValue>
}

export const Form = <TFormValues extends FieldValues>({ children, methods, submitHandler }: IFormProps<TFormValues>) => {

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(submitHandler)}>
        {children}
      </form>
    </FormProvider>

  )
}

export default Form

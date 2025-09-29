import { FormProvider } from 'react-hook-form'
import type { FieldValues, UseFormReturn, SubmitHandler } from 'react-hook-form'

interface IFormProps<TFormValue extends FieldValues> extends React.FormHTMLAttributes<HTMLFormElement> {
  methods: UseFormReturn<TFormValue, any, TFormValue>,
  submitHandler: SubmitHandler<TFormValue>
}

export const Form = <TFormValues extends FieldValues>({ children, methods, submitHandler, ...props }: IFormProps<TFormValues>) => {

  return (
    <FormProvider {...methods}>
      <form
        {...props}
        onSubmit={methods.handleSubmit(submitHandler)}>
        {children}
      </form>
    </FormProvider>

  )
}

export default Form
